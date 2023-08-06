#!/usr/bin/env python
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.special import logit, expit, digamma, polygamma
from scipy import stats
from scipy.optimize import minimize
from scipy import linalg


class Corncob():
    """
        A python class to implement corncob
        Covariates or X should at least include an intercept column = 1
        total and count should be a an array / series with one entry per observation
        These must be in the same length and orientation as covariates
        
    """
    def __init__(self, total, count, X=None, X_star=None, phi_init=0.5):
        # Assertions here TODO
        
        self.total = total
        self.count = count
        self.X = X
        self.X_star = X_star
        self.n_param_abd = len(X.columns)
        self.n_param_disp = len(X_star.columns)
        self.n_ppar = len(X.columns) + len(X_star.columns)
        self.df_model = self.n_ppar
        self.df_residual = len(X) - self.df_model
        
        if (self.df_residual) < 0:
            raise ValueError("Model overspecified. Trying to fit more parameters than sample size.")
        
        self.param_names_abd = X.columns
        self.param_names_disp = X_star.columns
        self.phi_init = phi_init
        
        # Inits
        self.start_params = None
        # Final params set to none until fit
        self.theta = None
        self.params_abd = None
        self.params_disp = None
        self.converged = None
        self.method = None
        self.n_iter = None
        self.LogLike = None
        self.execution_time = None
        self.fit_out = None

    def corncob_init(self):
        m = sm.GLM(
            endog=pd.DataFrame([
                self.count, # Success
                self.total - self.count, # Failures
            ]).T,
            exog=self.X,
            family=sm.families.Binomial()
        ).fit()        
        return(
            list(m.params) + ([logit(self.phi_init)] * self.n_param_disp)
        )

    def params_to_b_bstar(self, params):
        return((
            pd.Series(
                np.array(params[:self.n_param_abd]),
                index=self.param_names_abd
            ),
            pd.Series(
                np.array(params[-1*self.n_param_disp:]),
                index=self.param_names_disp
            )
        ))
        
    def mu_phi(self, b, b_star):
        mu_wlink = np.matmul(
            self.X,
            b
        )
        phi_wlink = np.matmul(
            self.X_star,
            b_star
        )
        mu = expit(mu_wlink)
        phi = expit(phi_wlink) 
        
        return ((
            mu,
            phi
        ))
    
    def _ll_cc(self, b, b_star):
        W = self.count
        M = self.total
        (mu, phi) = self.mu_phi(b, b_star)
        a = mu*(1-phi)/phi
        b = (1-mu)*(1-phi)/phi
        LL = stats.betabinom.logpmf(
                k=W,
                n=M,
                a=a,
                b=b
            )
        
        return LL

    def _hessian_cc(self, b, b_star):
        W = self.count
        M = self.total        
        (mu, phi) = self.mu_phi(b, b_star)
        # define gam
        gam  = phi/(1 - phi)
        # Hold digammas
        dg1 = digamma(1/gam)
        dg2 = digamma(M + 1/gam)
        dg3 = digamma(M - (mu + W * gam - 1)/gam)
        dg4 = digamma((1 - mu)/gam)
        dg5 = digamma(mu/gam)
        dg6 = digamma(mu/gam + W)        

        # Hold partials - this part is fully generalized
        dldmu = (-dg3 + dg4 - dg5 + dg6)/gam
        dldgam = (-dg1 + dg2 + (mu - 1) * (dg3 - dg4) + mu * (dg5 - dg6))/(gam*gam)
        
        tg1 = polygamma(1, M - (mu + W * gam - 1)/gam)
        tg2 = polygamma(1, (1 - mu)/gam)
        tg3 = polygamma(1, mu/gam)
        tg4 = polygamma(1, mu/gam + W)
        tg5 = polygamma(1, 1/gam)
        tg6 = polygamma(1, M + 1/gam)
        dldmu2 = (tg1 - tg2 - tg3 + tg4)/np.power(gam, 2)
        dldgam2 = (2 * gam * dg1 + tg5 - 2 * gam * dg2 - tg6 + np.power(mu - 1, 2) * tg1 - 2 * gam * (mu - 1) * dg3 - np.power(mu, 2) * tg3 + np.power(mu, 2) * tg4 + np.power(mu - 1, 2) * (-1*tg2) + 2 * gam * (mu - 1) * dg4 - 2 * gam * mu * dg5 + 2 * gam * mu * dg6)/np.power(gam, 4)

        dldmdg = (gam * (dg3 - dg4 + dg5 - dg6) + (mu - 1) * (tg2 - tg1) + mu * (tg3 - tg4))/np.power(gam, 3)
        dpdb = self.X.T * (mu * (1 - mu) )
        dgdb = self.X_star.T * gam

        mid4 = dldmu * mu * (1 - mu) * (1 - 2 * mu)
        mid5 = dldgam * gam
        term4 = np.dot(
            self.X.T * mid4,
            self.X
        )
        term5 = np.dot(
            self.X_star.T * mid5,
            self.X_star
        )
        term1 = np.dot(
            dpdb,
            ((-1*dldmu2) * dpdb).T
        )
        term2 = np.dot(
            dpdb,
            ((-1*dldmdg) * dgdb).T
        )    
        term3 = np.dot(
            dgdb,
            ((-1*dldgam2) * dgdb).T
        )
        # Quadrants of hessian
        u_L = term1 - term4
        b_L = term2.T
        u_R = term2
        b_R = term3-term5
        return np.bmat([
            [u_L, u_R],
            [b_L, b_R]
        ])

    def _gradient_cc(self, b, b_star):
        W = self.count
        M = self.total        
        (mu, phi) = self.mu_phi(b, b_star)
        # define gam
        gam  = phi/(1 - phi)
        # Hold digammas
        dg1 = digamma(1/gam)
        dg2 = digamma(M + 1/gam)
        dg3 = digamma(M - (mu + W * gam - 1)/gam)
        dg4 = digamma((1 - mu)/gam)
        dg5 = digamma(mu/gam)
        dg6 = digamma(mu/gam + W)        

        # Hold partials - this part is fully generalized
        dldmu = (-dg3 + dg4 - dg5 + dg6)/gam
        dldgam = (-dg1 + dg2 + (mu - 1) * (dg3 - dg4) + mu * (dg5 - dg6))/(gam*gam)
        
        tmp_b = mu * (1 - mu) * dldmu
        tmp_bstar = gam * dldgam

        # Add in covariates
        g_b = np.matmul(
            tmp_b.T,
            self.X
        )
        g_bstar = np.matmul(
            tmp_bstar.T,
            self.X_star
        )

        return -1*np.array(
            list(g_b)+list(g_bstar)
        )

    # Required for optimization
    def loglikelihood(self, params):
        (b, b_star) = self.params_to_b_bstar(params)

        return -1*np.sum(
            self._ll_cc(
                b,
                b_star
            )
        )
    
    def gradient(self, params):
        (b, b_star) = self.params_to_b_bstar(params)
        return self._gradient_cc(
            b,
            b_star
        )
    
    def hessian(self, params):
        (b, b_star) = self.params_to_b_bstar(params)
        return self._hessian_cc(
            b,
            b_star
        )
    
    def waltdt(self):
        if self.theta is None:
            raise ValueError("No fitted parameters. Please run fit first")
        # Implicit else we have some parameters
        # Dataframes
        result_table_abd = pd.DataFrame(
            index=self.param_names_abd,
            columns=[
                'Estimate',
                'se',
                't',
                'p'
            ]
        )
        result_table_abd['Estimate'] = self.params_abd
        result_table_disp = pd.DataFrame(
            index=self.param_names_disp,
            columns=[
                'Estimate',
                'se',
                't',
                'p'
            ]
        )
        result_table_disp['Estimate'] = self.params_disp
        
        
        # Calculate SE
        try:
            hessian = self.hessian(
                self.theta
            )
            hessian_factored = linalg.cholesky(hessian)
            covMat = linalg.cho_solve(
                (hessian_factored, False),
                np.eye(hessian_factored.shape[ 0 ])
            )
        except:
            return(
                result_table_abd,
                result_table_disp
            )
        # Implicit else we could calculate se
        se = np.sqrt(np.diag(covMat))
        # Tvalues
        tvalue = self.theta/se
        # And pvalues
        pval = stats.t.sf(np.abs(tvalue), self.df_residual)*2

        
        result_table_abd['se'] = se[:self.n_param_abd]
        result_table_abd['t'] = tvalue[:self.n_param_abd]
        result_table_abd['p'] = pval[:self.n_param_abd]        

        result_table_disp['se'] = se[-1*self.n_param_disp:]
        result_table_disp['t'] = tvalue[-1*self.n_param_disp:]
        result_table_disp['p'] = pval[-1*self.n_param_disp:]
        
        return((
            result_table_abd,
            result_table_disp
        ))
    
    def fit(self, start_params=None, maxiter=10000, maxfun=5000, method='trust-constr', **kwds):
        if start_params == None:
            # Reasonable starting values
            start_params = self.corncob_init()
        # scipy minimize
        minimize_res = minimize(
            fun=self.loglikelihood,
            method=method,
            x0=start_params,
            jac=self.gradient,
            hess=self.hessian,
        )
        self.fit_out = minimize_res
        self.theta = minimize_res.x
        self.params_abd = minimize_res.x[:self.n_param_abd]
        self.params_disp = minimize_res.x[-1*self.n_param_disp:]
        self.converged = minimize_res.success
        self.method = method
        #self.n_iter = minimize_res.cg_niter
        self.LogLike = -1*minimize_res.fun
        #self.execution_time = minimize_res.execution_time
        
        return minimize_res