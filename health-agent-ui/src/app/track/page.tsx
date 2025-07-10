"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import Navbar from "@/components/Navbar";

export default function TrackProgressPage() {
  const [userId, setUserId] = useState("");
  const [userName, setUserName] = useState("");
  const [update, setUpdate] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!userId || !userName || !update) {
      toast.error("All fields are required");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/track-progress`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uid: userId,
          name: userName,
          update: update,
        }),
      });

      if (!res.ok) throw new Error("Failed");

      toast.success("Progress saved successfully");
      setUpdate("");
    } catch (err) {
      toast.error("Failed to submit progress");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-xl mx-auto px-4 py-10">
        <Navbar/>
      <h1 className="text-2xl font-bold mb-6">📝 Track Your Progress</h1>

      <div className="space-y-4">
        <Input
          placeholder="User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <Input
          placeholder="Your Name"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
        />
        <Textarea
          placeholder="What did you accomplish today?"
          value={update}
          onChange={(e) => setUpdate(e.target.value)}
        />
        <Button onClick={handleSubmit} disabled={loading} className="w-full">
          {loading ? "Submitting..." : "Submit Progress"}
        </Button>
      </div>
    </main>
  );
}
