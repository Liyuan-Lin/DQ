DQ_VaR <- function(alpha, loss_ratio) {
    
    # alpha: quantile
    # lossRatio: 2-dimension vector of loss ratio
    
    n_stock <- nrow(loss_ratio)
    n_data <- ncol(loss_ratio)

    VaR <- numeric(n_stock)
  
    for (i in 1:n_stock) {
        VaR[i] <- quantile(loss_ratio[i,], 1 - alpha)
    }
    
    DQ_VaR <- (sum(colSums(loss_ratio) > sum(VaR))) / n_data / alpha
    
    print(loss_ratio)
    print(VaR)

    return(DQ_VaR)
}

DQ_ES <- function(alpha, loss_ratio) {

    # alpha: quantile
    # lossRatio: 2-dimension vector of loss ratio
    
    n_stock <- nrow(loss_ratio)
    n_data <- ncol(loss_ratio)

    ES <- numeric(n_stock)
  
    for (i in 1:n_stock) {
        ES[i] <- mean(loss_ratio[i, loss_ratio[i,] > quantile(loss_ratio[i,], 1 - alpha)])
    }
    
    Y <- loss_ratio - ES

    print(dim(Y))
    print(loss_ratio)
    print(ES)
  
    return(DQ_ES)

}

# generate random loss ratio
loss_ratio <- matrix(rnorm(25), nrow = 5, ncol = 5)

# test
DQ_VaR(0.2, loss_ratio)