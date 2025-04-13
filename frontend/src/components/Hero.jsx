import React from "react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import "../index.css";

function Hero() {
  return (
    <div className="relative bg-white dark:bg-gray-900 overflow-hidden min-h-[300px]">
      <div className="absolute inset-0 overflow-hidden">
      <div
          className="absolute right-0 top-1/2 translate-x-1/2  w-[800px] h-[800px]"
          style={{
            background:
              "radial-gradient(circle,  rgba(96, 165, 250, 0.2) 0%, transparent 70%)",
          }}
        />
        <div
          className="absolute left-0 top-1/2 -translate-x-1/2  -translate-y-1/2 w-[800px] h-[800px]"
          style={{
            background:
              "radial-gradient(circle,  rgba(96, 165, 250, 0.2) 0%, transparent 70%)",
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto">
        <div className="relative pb-8 bg-transparent sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="sm:text-center lg:text-left">
              <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
                <span className="block xl:inline">Enhance Your AI with</span>{" "}
                <span className="block text-primary dark:text-primary-light xl:inline">
                  Retrieval Augmented Generation
                </span>
              </h1>
              <p className="mt-3 text-base text-gray-500 dark:text-gray-300 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Empower your AI models with the ability to retrieve and leverage
                external knowledge, enhancing their responses and capabilities.
              </p>
              <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div className="rounded-md ">
                  <Link to={"/Signup"}>
                    <Button size="lg">Get Started</Button>
                  </Link>
                </div>
                <div className="mt-3 sm:mt-0 sm:ml-3">
                  <Button variant="outline" className="" size="lg">
                    Learn More
                  </Button>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default Hero;
