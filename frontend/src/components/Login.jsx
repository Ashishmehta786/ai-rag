import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  InfoIcon,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowLeft,
  Loader,
  Loader2,
  Loader2Icon,
} from "lucide-react";
import google from "../assets/google.svg";
import { useNavigate } from "react-router-dom";
import { CreateUser } from "../hooks/ZodHook";
import { ToastContainer } from "react-toastify";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from "../hooks/Firebase";
function Login() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const navigator = useNavigate();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (formData.password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    CreateUser(formData.name, formData.email, formData.password).then((res) => {
      if (res[0]) {
        setError(res[0].message);
      } else {
        setError("");
        setSuccess(true);
      }
    });
    setFormData({ name: "", email: "", password: "" });
    setLoading(true);
    setTimeout(() => navigator("/dashboard"), 1000);
  };
  const Signinwithgoogle = async () => {
    const provider = new GoogleAuthProvider();
    const res = await signInWithPopup(auth, provider);
    if (!res.user) {
      setError("something went wrong");
    }
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 ">
      <ToastContainer position="top-right" />
      <Button
        variant="ghost"
        className="absolute top-4 left-4 flex items-center text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:bg-gray-900"
        onClick={() => navigator("/")}
      >
        <ArrowLeft className="mr-2 h-5 w-5" /> Back to Home
      </Button>
      <div className="sm:mx-auto sm:w-full sm:max-w-2xl">
        <h2 className="mt-6 text-center text-2xl md:text-3xl leading-2 dark:text-white  font-bold text-gray-900">
          Welcome Back !
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="border-none  outline-none shadow-none dark:bg-transparent bg-white/80 backdrop-blur-sm">
          <CardContent>
            <div
              className="flex justify-center bg-gray-50 p-2 rounded-md dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-900/70 mb-6 cursor-pointer"
              onClick={Signinwithgoogle}
            >
              Login with Google {""}
              <img src={google} alt="logo" className="h-5 w-5 ml-2" />
            </div>
            <div>
              <div className="flex items-center">
                <div className="h-px flex-1 bg-neutral-900"></div>
                <span className="flex-shrink mx-4 text-gray-400 font-semibold">
                  or
                </span>
                <div className="h-px flex-1 bg-neutral-900"></div>
              </div>
            </div>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label
                  htmlFor="name"
                  className="text-sm font-medium text-gray-700 dark:text-white"
                >
                  Name
                </Label>
                <div className="relative">
                  <User
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary"
                    size={20}
                    strokeWidth={2}
                  />
                  <Input
                    id="name"
                    name="name"
                    type="text"
                    autoComplete="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="pl-10 bg-white/50 border-gray-300 focus:border-primary focus:ring-primary dark:bg-transparent dark:border-gray-800 dark:focus:border-gray-700 dark:focus:ring-gray-900"
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="email"
                  className="text-sm font-medium text-gray-700 dark:text-white"
                >
                  Email address
                </Label>
                <div className="relative">
                  <Mail
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary"
                    size={20}
                    strokeWidth={2}
                  />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="pl-10 bg-white/50 border-gray-300 focus:border-primary focus:ring-primary dark:bg-transparent dark:border-gray-800 dark:focus:border-gray-700 dark:focus:ring-gray-900"
                    placeholder="john@example.com"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label
                  htmlFor="password"
                  className="text-sm font-medium dark:text-white text-gray-700"
                >
                  Password
                </Label>
                <div className="relative">
                  <Lock
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary"
                    size={20}
                    strokeWidth={2}
                  />
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="pl-10 bg-white/50 border-gray-300 focus:border-primary focus:ring-primary dark:bg-transparent dark:border-gray-800 dark:focus:border-gray-700 dark:focus:ring-gray-900"
                    placeholder="••••••••"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff
                        className="h-5 w-5 text-primary"
                        strokeWidth={2}
                      />
                    ) : (
                      <Eye className="h-5 w-5 text-primary" strokeWidth={2} />
                    )}
                  </Button>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Password must be at least 8 characters long
                </p>
              </div>

              {error && (
                <Alert variant="destructive">
                  <InfoIcon className="h-5 w-5" strokeWidth={2} />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {success && (
                <Alert
                  variant="default"
                  className="bg-green-100 text-green-800 border-green-300"
                >
                  <InfoIcon className="h-5 w-5" strokeWidth={2} />
                  <AlertTitle>Success</AlertTitle>
                  <AlertDescription>
                    Account created successfully. Redirecting to dashboard...
                  </AlertDescription>
                </Alert>
              )}
              <Button
                type="submit"
                className={` ${
                  loading && "pointer-events-none opacity-50"
                } w-full bg-primary hover:bg-primary-dark dark:bg-white/90 dark:text-black dark:hover:bg-white/70 text-white relative flex `}
              >
                Login
                <div>
                  {loading && (
                    <Loader2Icon
                      className="w-4 h-4 text-neutral-100 animate-spin "
                      strokeWidth={2}
                    />
                  )}
                </div>
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <p className="text-center   dark:text-gray-400 text-sm text-gray-600 w-full">
              Don't have an account?{" "}
              <Button
                variant="link"
                className="p-0 h-auto font-medium text-primary"
                onClick={() => navigator("/signup")}
              >
                Signup
              </Button>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default Login;
