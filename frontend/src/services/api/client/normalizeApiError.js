import axios from 'axios'

export function normalizeApiError(error) {
  if (!axios.isAxiosError(error)) {
    return {
      type: 'UNKNOWN_ERROR',
      message: 'An unexpected error occurred.',
      statusCode: null,
      details: null,
    }
  }

  if (error.code === 'ERR_CANCELED') {
    return {
      type: 'REQUEST_CANCELED',
      message: 'Request was canceled.',
      statusCode: null,
      details: null,
    }
  }

  if (error.code === 'ECONNABORTED') {
    return {
      type: 'REQUEST_TIMEOUT',
      message: 'Request timed out. Please try again.',
      statusCode: null,
      details: null,
    }
  }

  if (!error.response) {
    return {
      type: 'NETWORK_ERROR',
      message: 'Unable to connect to the server.',
      statusCode: null,
      details: null,
    }
  }

  return {
    type: 'HTTP_ERROR',
    message: error.response?.data?.message ?? 'Request failed.',
    statusCode: error.response.status,
    details: error.response.data ?? null,
  }
}
