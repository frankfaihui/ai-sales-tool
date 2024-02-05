import config from "@/app/config";
import { cookies } from 'next/headers';

export async function POST(request: Request) {
  const body = await request.json()
  const response = await fetch(`${config.AI_SALES_API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  const json = await response.json();

  cookies().set({
    name: 'access_token',
    value: json.access_token,
    httpOnly: true,
    path: '/',
  });

  return Response.json({ success: true });
}
