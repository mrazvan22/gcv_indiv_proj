require("CCA")
require("CCP")
require("gplots")
#require("ggplot2")
require("Hmisc")
require("reshape")
# require("robust")
require("stats")

csv_to_mtx <- function(fpath) {
    print(paste("reading: ", fpath))
    data <- read.table(fpath, sep=",", header=TRUE, fill=TRUE)
    print(data[1:3, 1:length(data)])
    
    if (is.na(data[2, length(data)])) {
        dnames <- names(data)
        data <- data[1:(length(data)-1)]
        names(data) <- dnames[2:length(data)]
        mtx = as.matrix(data)
    } else {
        #print(paste("our data is:", data))

        rnames <- data[1]
        data <- data[2:length(data)]
        mtx = as.matrix(data)
#         print(dim(mtx))
#         print(dim(rnames))
        #if (dim(rnames)[1] == 1) {
        #    rnames <- t(rnames)
        #}
#         print(dim(rnames))
#         print(dim(mtx))
        rownames(mtx) <- t(rnames)
    }
    return(mtx)
}

remove_zerovar_cols <- function(mtx, outfile) {
  if (is.null(dim(mtx))) {
    return(mtx)
  }
  keep <- (apply(mtx, 2, var) != 0)
  if (sum(keep) != length(keep)) {
    writeLines(paste("the following columns had zero variance and were not kept: ", 
        toString(colnames(mtx)[!keep])), outfile)
    mtx = mtx[,keep]
  }
  return(mtx)
}

get_wts <- function(X, Y, wtsfile) {
  if (!is.null(wtsfile)) {
    print(paste("weights given as", wtsfile))
    wts <- read.table(wtsfile)
    wts <- wts[,]
  } else {
    print("no weights given, assuming all ones")
    wts <- as.vector(rep(1, dim(X)[1]))
  }
}

calc_covar <- function(X, Y, method, wts) {
  if ((method != "None") && !is.null(wts)) {
    stop("instance weights cannot currently be used with a robust-covariance estimation method")
  }
  print(paste("dimX = ", dim(X)))
  print(paste("dimY = ", dim(Y)))
  if (method == "ReweightedMCD") {
    covres <- covRob(cbind(X, Y), corr = FALSE, na.action = na.fail, 
                     estim='weighted')
    allcov <- covres$cov
  } else if (method == "OrthogonalizedGK") {
    covres <- covRob(cbind(X, Y), corr = FALSE, na.action = na.fail, 
                     estim='pairwiseGK')
    allcov <- covres$cov
  } else if (method == "None") {
      print(dim(cbind(X,Y)))
      print(length(wts))
      print(dim(wts))
      allcov <- cov.wt(cbind(X, Y), wt=wts)
      allcov <- allcov$cov
#     allcov <- var(cbind(X, Y), na.rm = TRUE, use = "pairwise")
  } else {
    stop(paste("Unrecognized method string: ", method))
  }
  return(allcov)
}

# like rcc in the CCA package, but allow a unified covariance matrix
# to allow use with robust covariance matrix estimation
do_rcc <- function (X, Y, allcov, lambda1, lambda2) {
  ndimX <- dim(X)[2]
  ndimY <- dim(Y)[2]
  if (is.null(ndimX)) {
    ndimX <- 1
  }
  if (is.null(ndimY)) {
    ndimY <- 1
  }
  Cxx <- allcov[1:ndimX, 1:ndimX] + diag(lambda1, max(1, ncol(X)))
  Cyy <- allcov[(ndimX+1):(ndimX+ndimY), (ndimX+1):(ndimX+ndimY)] + diag(lambda2, max(1, ncol(Y)))
  Cxy <- allcov[1:ndimX, (ndimX+1):(ndimX+ndimY)]
  
#   Cxx <- var(X, na.rm = TRUE, use = "pairwise") + diag(lambda1, ncol(X))
#   Cyy <- var(Y, na.rm = TRUE, use = "pairwise") + diag(lambda2, ncol(Y))
#   Cxy <- cov(X, Y, use = "pairwise")
  
  # the remaining code is from the function rcc in the CCA package
  Xnames <- dimnames(X)[[2]]
  Ynames <- dimnames(Y)[[2]]
  ind.names <- dimnames(X)[[1]]
  res <- geigen(Cxy, Cxx, Cyy)
  names(res) <- c("cor", "xcoef", "ycoef")
  scores <- comput(X, Y, res)
  return(list(cor = res$cor, names = list(Xnames = Xnames, 
    Ynames = Ynames, ind.names = ind.names), xcoef = res$xcoef, 
    ycoef = res$ycoef, scores = scores))
}

gen_data_for_match_permtest <- function(mtx1, mtx2, wts, robust_var_method,
    reg_params, name, out_dir, run_id, nperm) {
  
  out_prefix = file.path(out_dir, paste(name, toString(run_id), sep='_'))
#   permvec_file = paste(out_prefix, "permutations", sep="_")
  for (permnum in 1:nperm) {
    t_start = proc.time()
    print(paste("running permutation", permnum, "of", nperm))
    perm_prefix <- paste(out_prefix, "_perm", toString(permnum), sep='_')
    permvec <- sample(dim(mtx1)[1])
#     writeLines(toString(permvec), permvec_file)
    mtx1p <- mtx1[permvec,]
    rownames(mtx1p) <- rownames(mtx1)
    allcov <- calc_covar(mtx1p, mtx2, robust_var_method, wts)
    cc_res <- do_rcc(mtx1p, mtx2, allcov, reg_params[1], reg_params[2])
#     corr_YX <- cc_res$scores$corr.Y.xscores
#     corr_XY <- cc_res$scores$corr.X.yscores
#     write.csv(corr_YX, paste(perm_prefix, "YX-variate-corr.csv"), sep='_')
#     write.csv(corr_XY, paste(perm_prefix, "XY-variate-corr.csv"), sep='_')
#     write.csv(mtx1p, paste(perm_prefix, "X-variables.csv"))
    write.csv(cc_res$xcoef, paste(perm_prefix, 'X-weights.csv', sep='_'))
    write.csv(cc_res$ycoef, paste(perm_prefix, 'Y-weights.csv', sep='_'))
    write.csv(cc_res$cor, paste(perm_prefix, "canonical-correlations.csv", sep='_'))
    cat(permvec, file=paste(perm_prefix, "permutation.txt", sep='_'))
    print(paste("runtime for this permutation:", toString(proc.time() - t_start)))
  }
}

analyze_correlation <- function(fpath1, fpath2, name, regularize=FALSE, 
                                reg_params=NULL, robust_var_method="None",
                                xtform=NULL, ytform=NULL, 
                                norm_xrows=FALSE, norm_yrows=FALSE,
                                xkeep_attrs=NULL, ykeep_attrs=NULL,
                                scale_data=FALSE, wtsfile=NULL,
                                perm_out_dir=NULL, perm_run_id=NULL, nperm=NULL) {
    
    permparam_nullcount = is.null(perm_out_dir) + is.null(perm_run_id) + 
      is.null(nperm)
    if ((permparam_nullcount != 0) && (permparam_nullcount != 3)) {
      stop(paste("if any of the permutation parameters (perm_out_dir, ",
        "perm_run_id, nperm) are specified, they must all be specified.",
        sep=""))
    }
    run_permtest <- (permparam_nullcount == 0)
    
    mtx1 = csv_to_mtx(fpath1)
    mtx2 = csv_to_mtx(fpath2)
    print(paste("table 1 dimensions: ", toString(dim(mtx1))))
    print(paste("table 2 dimensions: ", toString(dim(mtx2))))
    
    outfile<-file(paste(name, ".txt", sep=""), open="wt")
    writeLines(paste("data1: ", fpath1), outfile)
    writeLines(paste("data2: ", fpath2), outfile)
    
    if (!is.null(xkeep_attrs)) {
      xkeep <- colnames(mtx1) %in% xkeep_attrs
      writeLines(paste("removing x-attributes: ", colnames(mtx1)[!xkeep]), outfile)
      remaining_names <- colnames(mtx1)[xkeep]
      mtx1 <- mtx1[,xkeep]
      mtx1 <- data.frame(mtx1)
      colnames(mtx1) <- remaining_names
    }
    if (!is.null(ykeep_attrs)) {
      ykeep <- colnames(mtx2) %in% ykeep_attrs
      writeLines(paste("removing y-attributes: ", colnames(mtx2)[!ykeep]), outfile)
      remaining_names <- colnames(mtx2)[ykeep]
      mtx2 <- mtx2[,ykeep]
      mtx2 <- data.frame(mtx2)
      colnames(mtx2) <- remaining_names
    }
    writeLines(paste("instance-name mismatches: ", 
        sum(rownames(mtx1) != rownames(mtx2)) ), outfile)
    
    n_indep_orig <- dim(mtx1)[2]
    n_dep_orig <- dim(mtx2)[2]
    mtx1 <- remove_zerovar_cols(mtx1, outfile)
    mtx2 <- remove_zerovar_cols(mtx2, outfile)
    if (!is.null(xtform)) {
      mtx1 = xtform(mtx1)
      writeLines(paste("x-transform:", toString(body(xtform))), outfile)
    } else {
      writeLines(paste("x-transform: (none)"), outfile)
    }
    if (!is.null(ytform)) {
      mtx2 = ytform(mtx2)
      writeLines(paste("y-transform:", toString(body(ytform))), outfile)
    } else {
      writeLines(paste("y-transform: (none)"), outfile)
    }
    
    if (norm_xrows) {
      writeLines(paste("normalizing x-rows"), outfile)
      mtx1 <- diag(1/rowSums(mtx1)) %*% mtx1
      mtx1[is.na(mtx1)] <- 0
    } else {
      writeLines(paste("not normalizing x-rows"), outfile)
    }
    
    if (norm_yrows) {
      writeLines(paste("normalizing y-rows"), outfile)
      mtx2 <- diag(1/rowSums(mtx2)) %*% mtx2
      mtx2[is.na(mtx2)] <- 0
    } else {
      writeLines(paste("not normalizing y-rows"), outfile)
    }
    
    if (scale_data) {
      writeLines("scaling X and Y", outfile)
      mtx1 = scale(mtx1, center = TRUE, scale = TRUE)
      mtx2 = scale(mtx2, center = TRUE, scale = TRUE)
    } else {
      writeLines("not scaling X and Y", outfile)
    }
    
    if (!is.null(wtsfile)) {
      writeLines(paste("weights given as", wtsfile), outfile)
    } else {
      writeLines("no weights given, assuming all ones", outfile)
    }
    
#     cca_res = cancor(mtx1, mtx2)
#     print("CANOCOR:")
#     print("correlations:")
#     print(cca_res$cor)
#     print("xcoef:")
#     print(cca_res$xcoef)
#     print("ycoef:")
#     print(cca_res$ycoef)
    
    reg_type = "none"
    writeLines(paste("robust covariance-estimation method:", robust_var_method), outfile)
    wts <- get_wts(mtx1, mtx2, wtsfile)
    allcov <- calc_covar(mtx1, mtx2, robust_var_method, wts)
    write.csv(allcov, paste(name, '_covar.csv', sep=''))
    if (regularize) {
      reg_type = "given"
      if (is.null(reg_params)) {
#         cov_prev <- cov
#         cov <- stats::cov
        print("estimating regularization coefficients...")
        reg_est = estim.regul(mtx1, mtx2)
        dev.copy(png,paste(name, "_reg_est.png", sep=""))
        dev.off()
  #       print(paste("estimated regularization coefficients are ",
  #         reg_est$lambda1, " and ", reg_est$lambda2))
        reg_params = c(reg_est$lambda1, reg_est$lambda2)
        reg_type = "auto-estimated"
#         cov <- cov_prev
      }
      name <- paste(name, "_reg=[", toString(reg_params), "]", sep="")
    } else {
      reg_params <- c(0, 0)
    }
    cc_res <- do_rcc(mtx1, mtx2, allcov, reg_params[1], reg_params[2])
    
    print("CCA:")
    print(cc_res$cor)
    print(cc_res$xcoef)
    print(cc_res$ycoef)
    #print(cc_res$scores)

    x_variates = cc_res$scores$xscores
    y_variates = cc_res$scores$yscores

    corr_XX = cc_res$scores$corr.X.xscores
    corr_YX = cc_res$scores$corr.Y.xscores
    corr_XY = cc_res$scores$corr.X.yscores
    corr_YY = cc_res$scores$corr.Y.yscores

    dims <- dim(mtx1)

    n_inst <- dim(mtx1)[1]
    n_indep <- dim(mtx1)[2]
    n_dep <- dim(mtx2)[2]

    print(paste("n_inst: ", n_inst))
    print(paste("n_indep: ", n_indep))
    print(paste("n_dep: ", n_dep))

    wilks_asym = p.asym(cc_res$cor, n_inst, n_indep, n_dep, tstat="Wilks")
    print(wilks_asym)
    asym_pvals = wilks_asym$p.value
    asym_max = max(which(asym_pvals < 0.1)) + 1
    asym_max = length(asym_pvals)
    print(asym_max)

    # n_permsample = 999
    # wilks_perm_pvals = c()
    # for (i in 1:asym_max) {
        # wilks_perm = p.perm(mtx1, mtx2, type="Wilks", nboot=n_permsample, rhostart=i)
        # wilks_perm_pvals = c(wilks_perm_pvals, wilks_perm$p.value)
    # }
	
	  hotelling_asym = p.asym(cc_res$cor, n_inst, n_indep, n_dep, tstat="Hotelling")
    print(hotelling_asym)
    asym_pvals = hotelling_asym$p.value
    asym_max = max(which(asym_pvals < 0.1)) + 1
    asym_max = length(asym_pvals)
    print(asym_max)

    # n_permsample = 999
    # hotelling_perm_pvals = c()
    # for (i in 1:asym_max) {
        # hotelling_perm = p.perm(mtx1, mtx2, type="Hotelling", nboot=n_permsample, rhostart=i)
        # hotelling_perm_pvals = c(hotelling_perm_pvals, hotelling_perm$p.value)
    # }
	
	  pillai_asym = p.asym(cc_res$cor, n_inst, n_indep, n_dep, tstat="Pillai")
    print(pillai_asym)
    asym_pvals = pillai_asym$p.value
    asym_max = max(which(asym_pvals < 0.1)) + 1
    asym_max = length(asym_pvals)
    print(asym_max)

    # n_permsample = 999
    # pillai_perm_pvals = c()
    # for (i in 1:asym_max) {
        # pillai_perm = p.perm(mtx1, mtx2, type="Pillai", nboot=n_permsample, rhostart=i)
        # pillai_perm_pvals = c(pillai_perm_pvals, pillai_perm$p.value)
    # }


    writeLines(paste("instances: ", n_inst), outfile)
    writeLines(paste("independent variables: ", n_indep, " (", n_indep_orig, 
        " before removing zero-variance variables)", sep=""), outfile)
    writeLines(paste("dependent variables: ", n_dep, " (", n_dep_orig, 
        " before removing zero-variance variables)", sep=""), outfile)
    if (regularize) {
      writeLines(paste("regularization type: ", reg_type), outfile)
      writeLines(paste("regularization lambda1: ", reg_params[1]), outfile)
      writeLines(paste("regularization lambda2: ", reg_params[2]), outfile)
    }
    writeLines(paste("canonical correlations: ", toString(cc_res$cor)), outfile)
    writeLines(paste("p-values (asymptotic Wilks):", toString(wilks_asym$p.value)), outfile)
    # writeLines(paste("p-values (permutation Wilks, ", toString(n_permsample), " resamples): ", toString(wilks_perm_pvals)), outfile)
	  writeLines(paste("p-values (asymptotic Hotelling):", toString(hotelling_asym$p.value)), outfile)
    # writeLines(paste("p-values (permutation Hotelling, ", toString(n_permsample), " resamples): ", toString(hotelling_perm_pvals)), outfile)
	  writeLines(paste("p-values (asymptotic Pillai):", toString(pillai_asym$p.value)), outfile)
    # writeLines(paste("p-values (permutation Pillai, ", toString(n_permsample), " resamples): ", toString(pillai_perm_pvals)), outfile)
    
    #print(corr_XY)
    #write.table(corr_XY, file=outfile, append=TRUE)
    #writeLines(toString(corr_XY), outfile)
    n_match = dim(corr_XY)[2]
    for (col_num in seq(1, n_match)) {
      cur_col_XY <- subset(corr_XY, select=col_num)
      cur_col_YX <- subset(corr_YX, select=col_num)
      #cur_col_XY <- cur_col_XY[order(cur_col_XY, decreasing=TRUE),] # doesn't stay for some reason
      #cur_cul_YX <- cur_col_YX[order(cur_col_YX, decreasing=TRUE),] # doesn't stay for some reason
      cur_canocor <- cc_res$cor[col_num]
      cur_cor_XX <- corr_XX[,col_num]
      cur_cor_YY <- corr_YY[,col_num]
      shared_var_X <- mean(cur_cor_XX**2)
      shared_var_Y <- mean(cur_cor_YY**2)
      redundancy_index_X <- shared_var_X * cur_canocor**2
      redundancy_index_Y <- shared_var_Y * cur_canocor**2
      
      writeLines(paste("__________________________________________________"), outfile)
      writeLines(paste("match ", col_num, ":"), outfile)
      writeLines(paste("canonical correlation: ", cur_canocor), outfile)
      writeLines(paste("canonical root: ", cur_canocor**2), outfile)
      #writeLines(paste("canonical X-loadings: ", toString(cur_cor_XX)), outfile)
      #writeLines(paste("canonical Y-loadings: ", toString(cur_cor_YY)), outfile)
      writeLines(paste("shared variance X: ", shared_var_X), outfile)
      writeLines(paste("shared variance Y: ", shared_var_Y), outfile)
      writeLines(paste("redundancy index X: ", redundancy_index_X), outfile)
      writeLines(paste("redundancy index Y: ", redundancy_index_Y), outfile)
      write.table(cur_col_XY[order(cur_col_XY, decreasing=TRUE),], file=outfile, append=TRUE)
      writeLines("-----", outfile)
      write.table(cur_col_YX[order(cur_col_YX, decreasing=TRUE),], file=outfile, append=TRUE)
      
      #latex(round(cur_col_XY[order(cur_col_XY, decreasing=TRUE),], digits=6), title=paste(name, "_XYcrossLoadings_", col_num, sep=""))
      #latex(round(cur_col_YX[order(cur_col_YX, decreasing=TRUE),], digits=6), title=paste(name, "_YXcrossLoadings_", col_num, sep=""))
    }
    
    close(outfile)
    
    write.csv(cc_res$xcoef, paste(name, 'X-weights.csv', sep='_'))
    write.csv(cc_res$ycoef, paste(name, 'Y-weights.csv', sep='_'))
    write.csv(corr_XX, paste(name, "XX-variate-corr.csv", sep='_'))
    write.csv(corr_YY, paste(name, "YY-variate-corr.csv", sep='_'))
    write.csv(corr_XY, paste(name, "XY-variate-corr.csv", sep='_'))
    write.csv(corr_YX, paste(name, "YX-variate-corr.csv", sep='_'))
    write.csv(mtx1, paste(name, "X-variables.csv", sep='_'))
    write.csv(mtx2, paste(name, "Y-variables.csv", sep='_'))
    write.csv(cc_res$cor, paste(name, 'canonical-correlations.csv', sep='_'))
    write.csv(as.matrix(mtx1) %*% cc_res$xcoef, paste(name, "X-variates.csv", sep='_'))
    write.csv(as.matrix(mtx2) %*% cc_res$ycoef, paste(name, "Y-variates.csv", sep='_'))

    if (run_permtest) {
      print("now running permutation tests.")
      gen_data_for_match_permtest(mtx1, mtx2, wts, robust_var_method,
        reg_params, name, perm_out_dir, perm_run_id, nperm)
    }
    
    if ( min(min(dim(mtx1)), min(dim(mtx2))) < 2 ) {
      print("X and/or Y variables are one-dimensional; cannot produce heatmaps.")
      return()
    }
    
    nclr <- 256
    colors <- bluered(nclr)

    plotwidth <- 15
    plotheight <- 15

    mval <- max(abs(cc_res$xcoef))
    brk <- seq(-mval, mval, length=nclr+1)
    pdf(paste(name, "_1_X-weights.pdf", sep=""), width=plotwidth, height=plotheight)
    # cellnote=round(cc_res$xcoef, digits=2), notecol="black", 
    heatmap.2(cc_res$xcoef, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="X weights", tracecol="black", trace="none")
    dev.off()

    mval <- max(abs(cc_res$ycoef))
    brk <- seq(-mval, mval, length=nclr+1)
    pdf(paste(name, "_2_Y-weights.pdf", sep=""), width=plotwidth, height=plotheight)
    heatmap.2(cc_res$ycoef, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="Y weights", tracecol="black", trace="none")
    dev.off()

    brk <- seq(-1, 1, length=nclr+1)

    pdf(paste(name, "_3_XX-variate-corr.pdf", sep=""), width=plotwidth, height=plotheight)
    heatmap.2(corr_XX, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="X->X variate corr", tracecol="black", trace="none")
    dev.off()

    pdf(paste(name, "_4_YY-variate-corr.pdf", sep=""), width=plotwidth, height=plotheight)
    heatmap.2(corr_YY, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="Y->Y variate corr", tracecol="black", trace="none")
    dev.off()

    pdf(paste(name, "_5_XY-variate-corr.pdf", sep=""), width=plotwidth, height=plotheight)
    heatmap.2(corr_XY, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="X->Y variate corr", tracecol="black", trace="none")
    dev.off()

    pdf(paste(name, "_6_YX-variate-corr.pdf", sep=""), width=plotwidth, height=plotheight)
    heatmap.2(corr_YX, col=colors, breaks=brk, Rowv=FALSE, Colv=FALSE, dendrogram="none", scale="none", main="Y->X variate corr", tracecol="black", trace="none")
    dev.off()
    
    
}

# analyze_correlation_regularized <- function(fpath1, fpath2, name) {
#   mtx1 = csv_to_mtx(fpath1)
#   mtx2 = csv_to_mtx(fpath2)
#   print(paste("table 1 dimensions: ", toString(dim(mtx1))))
#   print(paste("table 2 dimensions: ", toString(dim(mtx2))))
#   
#   reg_est = estim.regul(mtx1, mtx2)
#   print(reg_est)
# }


#assumes that the script is run from the code/ directory
setwd("../CCA_out2")
analyze_correlation('..//CCA_in//x_sample.csv', '..//CCA_in//y_sample.csv', 'toy1', regularize=TRUE, scale_data=TRUE)

