import config from "@/app/config";
import { NextRequest } from "next/server"
import { cookies } from 'next/headers';

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  const response = await fetch(`${config.AI_SALES_API_URL}/sales-pitches/${params.id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${cookies().get('access_token')?.value}`
    },
  })
  return new Response(response.body, response)
}
