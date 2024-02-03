import { Typography } from "@mui/material";
import SalesPitchForm from "./_components/SalesPitchForm";
import SalesPitchList from "./_components/SalesPitchList";
import styles from "./page.module.css";

export default async function Home() {

  return (
    <main className={styles.main}>
      <Typography variant="h4">Sales Pitch</Typography>
      <SalesPitchForm />
      <SalesPitchList />
    </main>
  );
}
