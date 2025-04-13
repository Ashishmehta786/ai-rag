import { useContext } from "react";
import { Authcontext } from "../contexts/Authcontext";
import SignupPage from "./Signup";
import { useNavigate } from "react-router-dom";

export default function Protectedroute({ children }) {
  const auth = useContext(Authcontext);
  const navigate = useNavigate();

  if (!auth.islogged) {
    navigate("/login");
  }

  return <div>{children}</div>;
}
