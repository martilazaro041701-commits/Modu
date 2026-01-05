import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="card">
      <p className="eyebrow">BARK | Body-Shop Analytics &amp; Reporting Kernel</p>
      <h1>Full-stack scaffold ready.</h1>
      <p className="lede">
        Django + DRF backend with MySQL hooks and a Vite React frontend. Update env files,
        start the API, then run the UI.
      </p>

      <div className="actions">
        <div>
          <p className="label">Backend</p>
          <code>cd backend && cp .env.example .env && ../.venv/bin/python manage.py runserver</code>
        </div>
        <div>
          <p className="label">Frontend</p>
          <code>cd frontend && npm install && npm run dev</code>
        </div>
      </div>

      <p className="lede">
        When both services are running, check the <Link to="/status">API status</Link> to verify the
        connection.
      </p>
    </section>
  );
}
