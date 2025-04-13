import React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import {
  Cpu,
  DatabaseZap,
  FileStack,
  FileText,
  TextSearch,
  TextSelect,
} from "lucide-react";
import "../index.css";
import { Cover } from "./ui/cover";
function HowItWorks() {
  const steps = [
    {
      title: "Data Ingestion",
      image: FileText,
      description:
        "Import and process large volumes of data from various sources.",
    },
    {
      title: "Indexing",
      image: TextSelect,
      description: "Create efficient indexes for quick information retrieval.",
    },
    {
      title: "Query Processing",
      image: Cpu,
      description: "Analyze user queries to understand intent and context.",
    },
    {
      title: "Information Retrieval",
      image: TextSearch,
      description: "Fetch relevant information from the indexed data.",
    },
    {
      title: "Content Generation",
      image: FileStack,
      description: "Combine retrieved information with AI-generated content.",
    },
    {
      title: "Output Refinement",
      image: DatabaseZap,
      description:
        "Polish and optimize the final output for coherence and relevance.",
    },
  ];

  return (
    <section
      id="how-it-works"
      className="py-12 bg-gray-50 dark:bg-gray-900 border-t border-gray-100 dark:border-gray-800 z-0 "
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:text-center">
          <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-neutral-300 sm:text-4xl">
            {" "}
            <div>
              <h1 className="text-4xl md:text-4xl lg:text-6xl font-semibold max-w-7xl mx-auto text-center mt-6 relative z-0 py-6 bg-clip-text text-transparent bg-gradient-to-b from-neutral-800 via-neutral-700 to-neutral-700 dark:from-neutral-800 dark:via-white dark:to-white ">
                How <Cover>Rag</Cover>
                Works
              </h1>
            </div>{" "}
          </p>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 dark:text-gray-400 lg:mx-auto">
            Understand the step-by-step process of Retrieval Augmented
            Generation.
          </p>
        </div>

        <div className="mt-10">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {steps.map((step, index) => (
              <Card
                key={step.title}
                className="hover:opacity-80 hover:ring-[8px] ring-gray-300/60 dark:hover:ring-gray-800/60 transition-all duration-500 bg-white dark:bg-gray-800/10 backdrop-blur-md bg-opacity-90 border border-gray-200 dark:border-gray-800  relative overflow-hidden group"
              >
                <div
                  className="absolute w-full h-full top-0 right-[70%]  group-hover:-right-[70%] transition-all duration-1000"
                  style={{
                    background:
                      "radial-gradient(circle,  rgba(96, 165, 250, 0.2) 0%, transparent 70%)",
                  }}
                ></div>
                <div
                  className="absolute w-full h-full top-0  left-[70%] group-hover:-left-[70%] transition-all duration-1000"
                  style={{
                    background:
                      "radial-gradient(circle,  rgba(96, 165, 250, 0.2) 0%, transparent 70%)",
                  }}
                ></div>

                <CardHeader className="">
                  <CardTitle className="flex items-center gap-2">
                    {`Step ${index + 1}: ${step.title}`}
                    <step.image />
                  </CardTitle>

                  {/* <img src={step.image} alt="" />
                   */}
                </CardHeader>
                <CardContent>
                  <CardDescription>{step.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default HowItWorks;
