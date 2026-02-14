import { loadEnv } from '../env/loadEnv'

const env = loadEnv()

export const appConfig = Object.freeze({
  app: {
    environment: env.appEnv,
    mode: env.mode,
  },
  api: {
    baseUrl: env.apiBaseUrl,
    timeoutMs: env.apiTimeoutMs,
  },
  logging: {
    level: env.logLevel,
  },
  featureFlags: {
    enableMap: env.enableMap,
    enableSaveProperty: env.enableSaveProperty,
  },
})
