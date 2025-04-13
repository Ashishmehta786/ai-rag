import { z } from "zod";
import { useQuery } from "../hooks/Query";

const ZodForm = async (email, password) => {
  const parsedData = z.object({
    email: z.string().email(),
    password: z.string().min(8),
  });
  if (!parsedData.safeParse({ email, password }).success) {
    return false;
  }
  const { ispending, error, data } = useQuery("auth", () => {
    fetch("http://localhost:8080/api/auth/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    }).then((res) => res.json());
  });
  return { ispending, error, data };
};

export default ZodForm;
