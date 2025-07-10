"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function DownloadReportPage() {
  const [loading, setLoading] = useState(false);
  const [reportUrl, setReportUrl] = useState("");

  // Replace with real userId later
  const userId = "123";

  const handleDownload = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/report/${userId}`);
      if (!res.ok) throw new Error("Failed to generate report");
      const data = await res.json();

      setReportUrl(data.url);
      window.open(`${process.env.NEXT_PUBLIC_API_BASE_URL}${data.url}`, "_blank");
      toast.success("Report opened in new tab.");
    } catch (err) {
      console.error(err);
      toast.error("Could not generate report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-xl mx-auto px-4 py-10">
        <Navbar/>
      <h1 className="text-2xl font-bold mb-6">📄 Download Your Health Report</h1>

      <Button onClick={handleDownload} disabled={loading} className="w-full">
        {loading ? "Generating..." : "Download PDF Report"}
      </Button>

      {reportUrl && (
        <p className="mt-4 text-sm text-muted-foreground">
          Your report is also available at:{" "}
          <a
            href={`http://localhost:8000${reportUrl}`}
            download
            className="underline text-blue-600"
            >
            Download Report
        </a>

        </p>
      )}
    </main>
  );
}
