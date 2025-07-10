// app/progress/page.tsx
"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import Navbar from "@/components/Navbar";

export default function ProgressPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get("http://localhost:8000/progress/123")
      .then((res) => {
        console.log("Progress logs fetched:", res.data);
        setLogs(res.data);
      })
      .catch((err) => {
        console.error("Progress fetch error:", err);
        setError("Failed to load progress logs.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-2xl mx-auto p-6">
      <Navbar/>
      <h1 className="text-2xl font-bold mb-4">📋 Progress Logs</h1>

      {loading && <p>Loading...</p>}

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {logs.length === 0 && !loading && (
        <p className="text-gray-600">No logs found for this user.</p>
      )}

      <div className="space-y-4">
        {logs.map((log, index) => (
          <Card key={index}>
            <CardHeader className="text-sm text-gray-500">
              {log.timestamp}
            </CardHeader>
            <CardContent>
              <p className="text-base">{log.update}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </main>
  );
}
