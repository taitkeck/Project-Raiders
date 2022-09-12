import type { NextApiRequest, NextApiResponse } from "next"
import { APIFetch } from "../../../../../utils/api"
import { StatusCodes } from "http-status-codes"

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { path } = req.query
  req.query = {}
  const pathStr = Array.isArray(path) ? path.join("/") : path
  const response = await APIFetch(req, `cart/${pathStr}`, [StatusCodes.OK], {
    method: "DELETE",
    body: req.body,
  })
  res.send(response)
}
