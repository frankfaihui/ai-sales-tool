import httpProxy from 'http-proxy'

const API_URL = process.env.NEXT_PUBLIC_AI_SALES_API_URL

const proxy = httpProxy.createProxyServer()

// Make sure that we don't parse JSON bodies on this route:
export const config = {
  api: {
    bodyParser: false,
  },
}

export default (req: any, res: any) => {
  return new Promise((resolve: any, reject: any) => {
    proxy.web(req, res, { target: API_URL, changeOrigin: true }, (err) => {
      if (err) {
        return reject(err)
      }
      resolve()
    })
  })
}
