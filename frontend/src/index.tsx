import ReactDOM from "react-dom/client";
import React from "react";
import { Route, Routes, BrowserRouter } from "react-router-dom";
import App from "./routes/App/App";
import PageNotFound from "./routes/404Page/404Page";

const Router: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);
root.render(<Router />);
