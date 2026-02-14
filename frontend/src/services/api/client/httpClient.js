import axios from 'axios'
import { appConfig } from '../../../config/runtime/appConfig'
import { logger } from '../../../shared/lib/logger/logger'
import { normalizeApiError } from './normalizeApiError'

function getRequestId() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID()
  }

  return `${Date.now()}-${Math.floor(Math.random() * 100000)}`
}

export const httpClient = axios.create({
  baseURL: appConfig.api.baseUrl,
  timeout: appConfig.api.timeoutMs,
  headers: {
    'Content-Type': 'application/json',
  },
})

httpClient.interceptors.request.use(
  (config) => {
    const requestId = getRequestId()

    config.headers['X-Request-Id'] = requestId

    logger.debug('API request started', {
      module: 'api-client',
      action: 'request',
      requestId,
      context: {
        method: config.method,
        url: config.url,
      },
    })

    return config
  },
  (error) => {
    const normalizedError = normalizeApiError(error)

    logger.error('API request configuration failed', {
      module: 'api-client',
      action: 'request-config-error',
      context: normalizedError,
    })

    return Promise.reject(normalizedError)
  },
)

httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const normalizedError = normalizeApiError(error)

    logger.warn('API response failed', {
      module: 'api-client',
      action: 'response-error',
      context: {
        statusCode: normalizedError.statusCode,
        type: normalizedError.type,
        message: normalizedError.message,
      },
    })

    return Promise.reject(normalizedError)
  },
)
