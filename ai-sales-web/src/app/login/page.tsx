'use client';
import { useState } from "react";
import { Box, TextField, Typography } from "@mui/material";
import styles from "../page.module.css";
import { LoadingButton } from "@mui/lab";
import { useRouter } from "next/navigation";
import { toast } from 'react-toastify';

export default function Page() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    try {
      setLoading(true);
      const response = await fetch(`/api/login`,
        {
          method: 'POST',
          body: JSON.stringify({ username, password }),
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 200) {
        toast.success('Login Successful', { autoClose: 2000 });
        router.push('/');
      }
    } catch (error) {
      toast.error('Login Failed', { autoClose: 2000 });
      console.error('Error:', error);
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <Box sx={{ width: 'min(80vw, 500px)' }}>
        <Typography variant="h5" component="div" gutterBottom color="black">
          Login to AI Sales Tool
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Username"
            variant="outlined"
            fullWidth
            margin="normal"
            value={username}
            placeholder="Any Fake Email"
            disabled={loading}
            required
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            placeholder="Any Fake Password"
            disabled={loading}
            required
            onChange={(e) => setPassword(e.target.value)}
          />
          <LoadingButton type="submit" variant="contained" color="primary" fullWidth loading={loading}>
            Login
          </LoadingButton>
        </form>
      </Box>
    </main>
  );
}
