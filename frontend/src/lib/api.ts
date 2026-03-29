import axios from 'axios'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
const FRONTEND_URL = process.env.NEXT_PUBLIC_FRONTEND_URL || 'http://localhost:3000'

export const backendApi = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const frontendApi = axios.create({
  baseURL: FRONTEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// TaxMaster API
export const taxMasterApi = {
  calculateTax: async (data: any) => {
    const response = await backendApi.post('/tax-master/calculate-tax', data)
    return response.data
  },
  compareRegimes: async (data: any) => {
    const response = await backendApi.post('/tax-master/compare-regimes', data)
    return response.data
  },
  getSection: async (sectionId: string) => {
    const response = await backendApi.get(`/tax-master/section/${sectionId}`)
    return response.data
  },
}

// FIRE Planner API
export const yojanaApi = {
  calculateFIRE: async (data: any) => {
    const response = await backendApi.post('/retirement-pro/fire-number', data)
    return response.data
  },
}

// Stock Quotes API
export const bazaarApi = {
  getStockQuote: async (data: any) => {
    const response = await backendApi.post('/stock-insight/stock-quote', data)
    return response.data
  },
}

// Health Score API
export const dhanApi = {
  calculateHealthScore: async (data: any) => {
    const response = await backendApi.post('/money-health/health-score', data)
    return response.data
  },
}

// PortfolioWise API
export const portfolioWiseApi = {
  calculateXIRR: async (data: any) => {
    const response = await backendApi.post('/portfolio-wise/xirr', data)
    return response.data
  },
  analyzePortfolio: async (data: any) => {
    const response = await backendApi.post('/portfolio-wise/analyze', data)
    return response.data
  },
}

// Life Event API
export const lifeEventApi = {
  planEvent: async (data: any) => {
    const response = await backendApi.post('/life-goals/plan', data)
    return response.data
  },
  getEventTypes: async () => {
    const response = await backendApi.get('/life-goals/types')
    return response.data
  },
}

// Couple Planner API
export const couplePlannerApi = {
  planFinances: async (data: any) => {
    const response = await backendApi.post('/partner-finance/finances', data)
    return response.data
  },
  splitExpense: async (data: any) => {
    const response = await backendApi.post('/partner-finance/split-expense', data)
    return response.data
  },
}

// ComplianceHelper API
export const complianceHelperApi = {
  getDisclaimers: async () => {
    const response = await backendApi.get('/compliance-helper/disclaimers')
    return response.data
  },
}

// Query Routing API
export const coordinatorApi = {
  route: async (query: string) => {
    const response = await backendApi.post('/coordinator/route', { query })
    return response.data
  },
}

// Format currency in INR
export const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount)
}

// Format percentage
export const formatPercent = (value: number) => {
  return `${value.toFixed(2)}%`
}

// Backward-compatible aliases
export const karvidApi = taxMasterApi
export const niveshakApi = portfolioWiseApi
export const vidhiApi = complianceHelperApi
