"use client";
import { useState } from "react";
import axios from "axios";
import Navbar from "@/components/Navbar";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";

export default function Home() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://localhost:8000/generate-plan", {
        input,
        name: "Muniba",
        uid: 123,
      });
      console.log("✅ PLAN RESPONSE:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("❌ PLAN ERROR:", err);
      setError("Something went wrong while generating the plan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto p-6">
      <Navbar />

      <h1 className="text-2xl font-bold mb-4 mt-4">💪 Health Planner Agent</h1>

      <Textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="e.g. I want to lose 5kg in 2 months..."
        rows={4}
        className="mb-2"
      />

      <Button onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Get Plan"}
      </Button>

      {error && (
        <Alert variant="destructive" className="mt-4">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <div className="mt-6 space-y-4">
          {result.notes && (
            <Alert>
              <AlertTitle>📝 Notes</AlertTitle>
              <AlertDescription>{result.notes}</AlertDescription>
            </Alert>
          )}

          {result.meal_plan?.length > 0 && (
            <Card>
              <CardHeader>🍽️ Meal Plan</CardHeader>
              <CardContent>
                <ul className="list-disc pl-5">
                  {result.meal_plan.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {result.workout_plan?.length > 0 && (
            <Card>
              <CardHeader>🏋️ Workout Plan</CardHeader>
              <CardContent>
                <ul className="list-disc pl-5">
                  {result.workout_plan.map((item: string, i: number) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {typeof result === "string" && (
            <pre className="bg-gray-100 p-4 rounded border text-sm whitespace-pre-wrap">
              {result}
            </pre>
          )}

          {typeof result === "object" &&
            !result.meal_plan &&
            !result.workout_plan &&
            !result.notes && (
              <Alert className="bg-yellow-50 border-yellow-200 text-yellow-900">
                <AlertTitle>⚠️ Unstructured Response</AlertTitle>
                <AlertDescription>
                  <pre className="whitespace-pre-wrap text-sm">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </AlertDescription>
              </Alert>
            )}
        </div>
      )}
    </main>
  );
}
