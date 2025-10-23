import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Login from './pages/Login/Login.tsx';
import Signup from './pages/Signup/Signup.tsx';
import Homepage from './pages/Homepage/Homepage.tsx';
import CreateVacation from './pages/CreateVacation/CreateVacation.tsx';
import EditVacation from './pages/EditVacation/EditVacation.tsx';
import "../src/styles/main.scss"

let router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
    children: [
      {
        path: "/login",
        element: <Login/>,
      },
      {
        path: "/signup",
        element: <Signup/>,
      },
      {
        path: "/",
        element: <Homepage/>,
      },
      {
        path: "/create-vacation",
        element: <CreateVacation/>,
      },
      {
        path: "/edit-vacation/:id",
        element: <EditVacation/>,
      }
    ]
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />,
  </StrictMode>,
)
