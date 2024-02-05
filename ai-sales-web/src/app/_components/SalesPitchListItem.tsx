'use client';
import { Button, Card, CardActions, CardContent, Typography } from "@mui/material";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

export default function SalesPitchListItem(props: any) {
  const { pitch } = props;

  const route = useRouter();

  const handleClick = async () => {
    try {
      const response = await fetch(`/sales-pitches/${pitch._id}`, { method: 'DELETE' });

      if (response.status !== 200) {
        throw new Error('Failed to delete');
      }
      route.refresh();
    } catch (error) {
      toast.error('Failed to delete', { autoClose: 2000 });
      console.error('Error:', error);
    }
  }

  return (
    <Card sx={{ marginTop: '20px', marginBottom: '20px', width: 'min(80vw, 800px)' }}>
      <CardContent>
        <Typography variant="h5" component="div" color="black">
          Product: {pitch.product}
        </Typography>
        <Typography color="text.secondary">
          Audience: {pitch.audience}
        </Typography>
        <Typography color="text.secondary">
          {pitch.content}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" color="primary" onClick={handleClick}>
          Remove
        </Button>
      </CardActions>
    </Card>
  );
}

