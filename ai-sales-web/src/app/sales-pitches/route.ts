import config from "@/app/config";

export async function POST(request: Request) {
  const body = await request.json()
  const response = await fetch(`${config.AI_SALES_API_URL}/sales-pitches`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  return new Response(response.body, response)
}

