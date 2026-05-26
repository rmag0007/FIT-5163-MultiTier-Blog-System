import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import BlogHome from "./components/Blog/BlogHome";
import BlogPostPage from "./pages/BlogPostPage";
import CreatePost from "./pages/CreatePost";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<BlogHome />} />
        <Route path="/post/:id" element={<BlogPostPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/create-post" element={
          <PrivateRoute>
            <CreatePost />
          </PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}