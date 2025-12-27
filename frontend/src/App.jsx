import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ResumeOnly from "./pages/ResumeOnly";
import ResumeJD from "./pages/ResumeJD";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/resume-only" element={<ResumeOnly />} />
        <Route path="/resume-jd" element={<ResumeJD />} />
      </Routes>
    </BrowserRouter>
  );
}
