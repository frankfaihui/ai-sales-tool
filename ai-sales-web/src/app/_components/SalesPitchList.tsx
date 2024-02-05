import { Typography } from "@mui/material";
import SalesPitchListItem from "./SalesPitchListItem";
import config from "@/app/config";
import { redirect } from "next/navigation";
import { cookies } from 'next/headers';

export default async function SalesPitchList() {

  let json;
  try {
    const response = await fetch(`${config.AI_SALES_API_URL}/sales-pitches`, {
      cache: 'no-store',
      headers: {
        'Authorization': `Bearer ${cookies().get('access_token')?.value}`
      }
    });
    json = await response.json();

    if (response.status !== 200) {
      redirect('/login');
    }
  } catch (error) {
    console.error('Error:', error);
    redirect('/login');
  }

  return (
    <div>
      <Typography variant="h5" mt='50px' color="black">Sales Pitch List</Typography>
      {json.data.map((pitch: any) => (
        <SalesPitchListItem key={pitch._id} pitch={pitch} />
      ))}
    </div>
  );
}

