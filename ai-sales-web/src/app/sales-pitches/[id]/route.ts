import { NextRequest } from "next/server"

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_AI_SALES_API_URL}/sales-pitches/${params.id}`, {
    method: 'DELETE',
  })
  return new Response(response.body, response)
}
