import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useForm } from "react-hook-form";
import logo from "../assets/logo.png";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  InfoIcon,
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowLeft,
  Loader2Icon,
  Check,
  CheckCircleIcon,
} from "lucide-react";
import google from "../assets/google.svg";
import { useNavigate } from "react-router-dom";
import { CreateUser } from "../hooks/ZodHook";
import { ToastContainer } from "react-toastify";
import z from "zod";
import ZodForm from "../hooks/AuthHook";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from "../hooks/Firebase";
const formSchema = z.object({
  name: z
    .string()
    .min(3, { message: "Name must be at least 3 characters long" }),
  email: z.string().email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(1, { message: "Password must be at least 1 characters long" }),
});
function SignupPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "aa",
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
  const handleSubmit = (data) => {
    console.log(formData);
    setLoading(true);
    setError("");
    setSuccess(false);
    console.log("creating user");
    CreateUser(data.name, data.email, data.password).then((res) => {
      if (res[0]) {
        setError(res[0].message);
        setLoading(false);
        setFormData({ name: "", email: "", password: "" });
      } else {
        setError("");
        setSuccess(true);
        setTimeout(() => navigator("/dashboard"), 1000);
        setLoading(false);
      }
    });
    setFormData({ name: "", email: "", password: "" });
  };
  const Signinwithgoogle = async () => {
    const provider = new GoogleAuthProvider();
    const res = await signInWithPopup(auth, provider);
    if (!res.user) {
      setError("something went wrong");
    }
  };
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", email: "", password: "" },
  });
  function onSubmit(values) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(values, null, 2)}</code>
        </pre>
      ),
    });
  }
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 dark:from-primary-900 dark:to-secondary-900">
      <ToastContainer position="top-right" />
      <Button
        variant="ghost"
        className="absolute top-4 left-4 flex items-center text-gray-600 dark:text-gray-300
        dark:hover:bg-gray-900 hover:text-gray-900"
        onClick={() => navigator("/")}
      >
        <ArrowLeft className="mr-2 h-5 w-5" /> Back to Home
      </Button>
      <div className="sm:mx-auto sm:w-full sm:max-md">
        <h2 className="mt-6 text-center text-2xl md:text-3xl leading-2 dark:text-white  font-bold text-gray-900 flex justify-center items-center">
          Create your account and start exploring
          <img src={logo} alt="logo" className="h-8 w-8 ml-2" />
        </h2>
      </div>
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="border-none shadow-none bg-white/80 dark:bg-transparent backdrop-blur-sm">
          <CardContent>
            <div
              className="flex justify-center bg-gray-50 p-2 rounded-md dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-900/70 mb-6 cursor-pointer"
              onClick={Signinwithgoogle}
            >
              Sign up with Google {""}
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
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(handleSubmit)}
                className="space-y-6 error-neutral-100"
              >
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field, fieldState }) => (
                    <FormItem>
                      <FormLabel>
                        <Label
                          htmlFor="name"
                          className="text-sm font-medium text-gray-700 dark:text-gray-200"
                        >
                          Name
                        </Label>
                      </FormLabel>
                      <FormControl>
                        <div className="relative">
                          <User
                            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-primary "
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
                            {...field}
                          />{" "}
                        </div>
                      </FormControl>
                      <FormDescription>
                        Please enter your full name.
                      </FormDescription>
                      <FormMessage className="dark:text-red-600" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        <Label
                          htmlFor="email"
                          className="text-sm font-medium text-gray-700 dark:text-gray-200"
                        >
                          Email address
                        </Label>
                      </FormLabel>
                      <FormControl>
                        <>
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
                              {...field}
                            />
                          </div>
                        </>
                      </FormControl>
                      <FormDescription>
                        We'll never share your email with anyone else.
                      </FormDescription>
                      <FormMessage className="dark:text-red-600" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        {" "}
                        <Label
                          htmlFor="password"
                          className="text-sm font-medium text-gray-700 dark:text-gray-200"
                        >
                          Password
                        </Label>
                      </FormLabel>
                      <FormControl>
                        <>
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
                              {...field}
                              className="pl-10 bg-white/50 border-gray-300 focus:border-primary focus:ring-primary dark:bg-transparent dark:border-gray-800 dark:focus:border-gray-700 dark:focus:ring-gray-900"
                              placeholder="••••••••"
                            />
                            <Button
                              type="button"
                              variant="ghost"
                              size="icon"
                              className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent "
                              onClick={() => setShowPassword(!showPassword)}
                            >
                              {showPassword ? (
                                <EyeOff
                                  className="h-5 w-5 text-primary"
                                  strokeWidth={2}
                                />
                              ) : (
                                <Eye
                                  className="h-5 w-5 text-primary"
                                  strokeWidth={2}
                                />
                              )}
                            </Button>
                          </div>
                        </>
                      </FormControl>
                      <FormDescription>
                        Password must be at least 8 characters long
                      </FormDescription>
                      <FormMessage className="dark:text-red-600" />
                    </FormItem>
                  )}
                />
                <div className="space-y-2"></div>
                <div className="space-y-2"></div>
                <div className="space-y-2"></div>
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
                    <CheckCircleIcon
                      className="h-5 w-5 dark:text-green-800"
                      strokeWidth={2}
                    />
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
                  } w-full bg-primary hover:bg-primary-dark text-white relative flex dark:bg-white/90 dark:text-black  dark:hover:bg-white/80`}
                >
                  Create Account
                  <div>
                    {loading && (
                      <Loader2Icon className="w-4 h-4 animate-spin" />
                    )}
                  </div>
                </Button>
              </form>
            </Form>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <p className="text-center text-sm text-gray-600 dark:text-gray-400 w-full">
              By signing up, you agree to our{" "}
              <Button
                variant="link"
                className="p-0 h-auto font-medium text-primary"
              >
                Terms of Service
              </Button>{" "}
              and{" "}
              <Button
                variant="link"
                className="p-0 h-auto font-medium text-primary"
              >
                Privacy Policy
              </Button>
            </p>
            <p className="text-center text-sm text-gray-600 dark:text-gray-400 w-full">
              Already have an account?{" "}
              <Button
                variant="link"
                className="p-0 h-auto font-medium text-primary"
                onClick={() => navigator("/login")}
              >
                Log in
              </Button>
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default SignupPage;
