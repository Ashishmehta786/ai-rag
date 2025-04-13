import z from "zod";
import { toast } from "react-toastify";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "firebase/auth";
import { auth } from "./Firebase";
const UserSchema = z.object({
  name: z
    .string()
    .min(3, { message: "Name must be at least 3 characters long" }),
  email: z.string().email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters long" }),
});

const CreateUser = async (name, email, password) => {
  const user = UserSchema.safeParse({
    name,
    email,
    password,
  });
  if (!user.success) {
    toast.error(user.error.issues[0].message);
  }
  console.log(name, email, password);
  const User = await createUserWithEmailAndPassword(auth, email, password);
  const UserRes = User.user.email;
  return [user.error, UserRes];
};

const LoginUser = async (email, password) => {
  const user = UserSchema.safeParse({
    email,
    password,
  });
  if (!user.success) {
    toast.error(user.error.issues[0].message);
  }
  const User = await signInWithEmailAndPassword(auth, email, password);
  const UserRes = User.user.email;
  return [user.error, UserRes];
};

export { CreateUser, LoginUser };
