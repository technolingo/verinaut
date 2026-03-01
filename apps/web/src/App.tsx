import { useState } from 'react';
import reactLogo from '/react.svg';
import viteLogo from '/vite.svg';

import { Navbar } from './components/Navbar';


export const App = () => {
  const [count, setCount] = useState(0);

  return (
    <>
    <Navbar />
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-900 p-8 pt-16 text-white">
      <div className="mb-8 flex gap-8">
        <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Similique alias cum repudiandae illo repellendus iste atque mollitia, omnis itaque, aliquid debitis doloremque nulla ipsum quas ad fuga. Veritatis, beatae eius.</p>
      </div>
    </div>
    </>
  );
};
