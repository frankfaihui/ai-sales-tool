import { Typography } from "@mui/material";
import SalesPitchListItem from "./SalesPitchListItem";

export default async function SalesPitchList() {

  let json;
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_AI_SALES_API_URL}/sales-pitches`, { cache: 'no-store' });
    json = await response.json();
  } catch (error) {
    return null;
  }

  return (
    <div>
      <Typography variant="h5" mt='50px'>Sales Pitch List</Typography>
      {json.data.map((pitch: any) => (
        <SalesPitchListItem key={pitch._id} pitch={pitch} />
      ))}
    </div>
  );
}

