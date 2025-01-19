import React from 'react';

const Navbar = () => {
    return (
        <nav className="bg-zinc-800 p-4">
            <div className="container mx-auto flex justify-between items-center">
                <div className="text-white text-lg font-bold">
                    Captionize
                </div>
                <div className="space-x-4">
                    <a href="/" className="text-white">Home</a>
                    <a href="/about" className="text-white">About</a>
                    <a href="/contact" className="text-white">Contact</a>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;