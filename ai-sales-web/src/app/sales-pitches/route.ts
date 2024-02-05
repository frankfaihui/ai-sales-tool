import config from "@/app/config";
import { cookies } from 'next/headers';

export async function GET(request: Request) {
  const response = await fetch(`${config.AI_SALES_API_URL}/sales-pitches`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${cookies().get('access_token')?.value}`
    },
  })
  return new Response(response.body, response);
}

export async function POST(request: Request) {
  const body = await request.json()
  const response = await fetch(`${config.AI_SALES_API_URL}/sales-pitches`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${cookies().get('access_token')?.value}`
    },
    body: JSON.stringify(body),
  })
  return new Response(response.body, response);
}

