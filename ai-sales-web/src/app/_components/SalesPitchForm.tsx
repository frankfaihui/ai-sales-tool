'use client';
import { useState } from 'react';
import { TextField, Select, MenuItem, FormControl, InputLabel, SelectProps, TextFieldProps, Box } from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';

export default function SalesPitchForm() {
  const [product, setProduct] = useState('');
  const [audience, setAudience] = useState<SelectOption>('consumer');
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleProductChange: TextFieldProps['onChange'] = (event) => {
    setProduct(event.target.value);
  };

  const handleAudienceChange: SelectProps['onChange'] = (event) => {
    setAudience(event.target.value as SelectOption);
  };

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      const response = await fetch(`/sales-pitches`,
        {
          method: 'POST',
          body: JSON.stringify({ product, audience }),
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status !== 201) {
        throw new Error('Failed to create');
      }

      // clear input
      setProduct('');

      // refresh the page
      router.refresh();
    } catch (error) {
      toast.error('Failed to Create', { autoClose: 2000 });
      console.error('Error:', error);
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ width: 'min(80vw, 500px)' }}>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Product"
          variant="outlined"
          fullWidth
          value={product}
          onChange={handleProductChange}
          margin="normal"
          required
          disabled={loading}
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Audience</InputLabel>
          <Select
            value={audience}
            onChange={handleAudienceChange}
            label="Audience"
            disabled={loading}
          >
            <MenuItem value="consumer">Consumer</MenuItem>
            <MenuItem value="business">Business</MenuItem>
            {/* Add more audience options as needed */}
          </Select>
        </FormControl>

        <LoadingButton type="submit" variant="contained" color="primary" fullWidth loading={loading}>
          Generate
        </LoadingButton>
      </form>
    </Box>
  );
}

type SelectOption = 'consumer' | 'business';
