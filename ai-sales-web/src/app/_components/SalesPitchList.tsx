import { Typography } from "@mui/material";
import SalesPitchListItem from "./SalesPitchListItem";

export default async function SalesPitchList() {

  const response = await fetch('http://127.0.0.1:8080/sales-pitches', { cache: 'no-store' });
  const json = await response.json();

  return (
    <div>
      <Typography variant="h5" mt='50px'>Sales Pitch List</Typography>
      {json.data.map((pitch: any) => (
        <SalesPitchListItem key={pitch._id} pitch={pitch} />
      ))}
    </div>
  );
}

