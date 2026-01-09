import { useEffect, useState } from "react";
import { getHealth } from "../../../api/client";

export default function ApiStatus() {
  const [status, setStatus] = useState("Checking backend...");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await getHealth();
        setStatus(`API online: ${JSON.stringify(data)}`);
      } catch (error) {
        setStatus(
          "API unreachable. Start Django on http://localhost:8000 and confirm MYSQL_ env values."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
  }, []);

  return (
    <section className="card">
      <p className="eyebrow">API Status</p>
      <h1>Django + MySQL health</h1>
      <p className="lede">
        This checks the DRF health endpoint at `/api/health/`. Ensure your backend and MySQL are
        running.
      </p>

      <div className="status">
        <span className="dot" aria-hidden="true" data-loading={loading}></span>
        <span>{status}</span>
      </div>
    </section>
  );
}
