const APP_ENVS = ['development', 'staging', 'production']
const LOG_LEVELS = ['debug', 'info', 'warn', 'error', 'audit']

function parseBoolean(rawValue, fallbackValue = false) {
  if (rawValue === undefined || rawValue === null || rawValue === '') {
    return fallbackValue
  }

  return rawValue === 'true' || rawValue === '1'
}

function parsePositiveInteger(rawValue, fallbackValue) {
  if (rawValue === undefined || rawValue === null || rawValue === '') {
    return fallbackValue
  }

  const parsedValue = Number.parseInt(rawValue, 10)
  if (Number.isNaN(parsedValue) || parsedValue <= 0) {
    throw new Error(`[env] VITE_API_TIMEOUT_MS must be a positive integer. Received: ${rawValue}`)
  }

  return parsedValue
}

function inferAppEnv(viteEnv) {
  if (viteEnv.VITE_APP_ENV) {
    return viteEnv.VITE_APP_ENV
  }

  if (viteEnv.MODE === 'production') {
    return 'production'
  }

  if (viteEnv.MODE === 'staging') {
    return 'staging'
  }

  return 'development'
}

export function loadEnv(viteEnv = import.meta.env) {
  const appEnv = inferAppEnv(viteEnv)

  if (!APP_ENVS.includes(appEnv)) {
    throw new Error(`[env] VITE_APP_ENV must be one of: ${APP_ENVS.join(', ')}. Received: ${appEnv}`)
  }

  if (!viteEnv.VITE_API_BASE_URL) {
    throw new Error('[env] Missing required variable: VITE_API_BASE_URL')
  }

  const logLevel = viteEnv.VITE_LOG_LEVEL ?? (appEnv === 'development' ? 'debug' : 'info')

  if (!LOG_LEVELS.includes(logLevel)) {
    throw new Error(`[env] VITE_LOG_LEVEL must be one of: ${LOG_LEVELS.join(', ')}. Received: ${logLevel}`)
  }

  return Object.freeze({
    appEnv,
    mode: viteEnv.MODE,
    apiBaseUrl: viteEnv.VITE_API_BASE_URL,
    apiTimeoutMs: parsePositiveInteger(viteEnv.VITE_API_TIMEOUT_MS, 10000),
    logLevel,
    enableMap: parseBoolean(viteEnv.VITE_ENABLE_MAP, true),
    enableSaveProperty: parseBoolean(viteEnv.VITE_ENABLE_SAVE_PROPERTY, true),
  })
}
