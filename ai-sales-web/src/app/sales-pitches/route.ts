export async function POST(request: Request) {
  const body = await request.json()
  const response = await fetch(`${process.env.NEXT_PUBLIC_AI_SALES_API_URL}/sales-pitches`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })
  return new Response(response.body, response)
}

