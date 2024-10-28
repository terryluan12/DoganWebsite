"use client";

import { useEffect } from "react";

export default function Game() {
    
    useEffect(() => {
        const canvas = document.querySelector("#glcanvas") as HTMLCanvasElement;

        const gl = canvas?.getContext("webgl");

        const vsSource =`
                        attribute vec4 aVertexPosition;
                        uniform mat4 uModelViewMatrix;
                        uniform mat4 uProjectionMatrix;
                        void main() {
                            gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
                        }
                        `;
        const fsSource =`
                        void main() {
                            gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
                        }
                        `;

                      
        if(gl === null) {
            alert("Unable to initialize WebGL. Your browser may not support it.");
            return;
        }

        gl.clearColor(0.0, 0.0, 0.0, 1.0);

        gl.clear(gl.COLOR_BUFFER_BIT);
    }, [])
    
    return (
        <canvas id="glcanvas" width="640" height="480"> </canvas>
    );
  }
  