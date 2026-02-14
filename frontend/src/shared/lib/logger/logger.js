import { appConfig } from '../../../config/runtime/appConfig'

const LEVEL_PRIORITY = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
  audit: 50,
}

const REDACT_KEYS = ['password', 'token', 'authorization', 'email', 'phone']

function shouldLog(level) {
  return LEVEL_PRIORITY[level] >= LEVEL_PRIORITY[appConfig.logging.level]
}

function redactValue(value) {
  if (!value || typeof value !== 'object') {
    return value
  }

  if (Array.isArray(value)) {
    return value.map((item) => redactValue(item))
  }

  return Object.entries(value).reduce((accumulator, [key, fieldValue]) => {
    const isSensitive = REDACT_KEYS.some((redactKey) => key.toLowerCase().includes(redactKey))

    accumulator[key] = isSensitive ? '[REDACTED]' : redactValue(fieldValue)
    return accumulator
  }, {})
}

function buildPayload(level, message, metadata = {}) {
  return {
    timestamp: new Date().toISOString(),
    level,
    module: metadata.module ?? 'app',
    action: metadata.action ?? 'unknown',
    message,
    context: redactValue(metadata.context ?? {}),
    requestId: metadata.requestId,
  }
}

function emit(level, payload) {
  if (!shouldLog(level)) {
    return
  }

  if (level === 'error') {
    console.error(payload)
    return
  }

  if (level === 'warn') {
    console.warn(payload)
    return
  }

  console.log(payload)
}

function createLogMethod(level) {
  return (message, metadata) => {
    const payload = buildPayload(level, message, metadata)
    emit(level, payload)
  }
}

export const logger = {
  debug: createLogMethod('debug'),
  info: createLogMethod('info'),
  warn: createLogMethod('warn'),
  error: createLogMethod('error'),
  audit: createLogMethod('audit'),
}
