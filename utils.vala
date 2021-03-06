/*
Copyright (c) 2014, 2015, 2016, Ian Smith (m4r35n357)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
using Json;
using GLib.Math;

namespace Simulations {

    /**
     * Interface for the physical model (client)
     */
    public interface IModel : GLib.Object {
        /**
         * Coordinate updates, called by ISymplectic.compose()
         */
        public abstract void qUp (double d);

        /**
         * Momentum updates, called by ISymplectic.compose()
         */
        public abstract void pUp (double c);

        /**
         * Sole method called by main(), calls ISymplectic.compose() method on the integrator as needed
         */
        public abstract void solve ();
    }

    /**
     * Interface for the integrators
     */
    public interface ISymplectic : GLib.Object {
        /**
         * Should be called by IModel.solve() as needed, calls IModel.pUp() and IModel.qUp()
         */
        public abstract void compose ();
    }

    /**
     * Parse JSON initial conditions data from stdin
     */
    private static Json.Object getJson () {
        var input = new StringBuilder();
        var buffer = new char[1024];
        while (!stdin.eof()) {
            var chunk = stdin.gets(buffer);
            if (chunk != null) {
                input.append(chunk);
            }
        }
        unowned Json.Object obj;
        var p = new Parser();
        try {
            p.load_from_data(input.str);
            obj = p.get_root().get_object();
        } catch (Error e) {
            stderr.printf("Unable to parse the input data: %s\n", e.message);
            return_if_reached();
        }
        return obj;
    }

    /**
     * Used by all models
     */
    private static double logError (double e) {
        return 10.0 * log10(e > 1.0e-18 ? e : 1.0e-18);
    }

    /**
     * Entry point
     */
    public static int main (string[] args) {
        var arg0 = args[0].split("/");
        switch (arg0[arg0.length - 1]) {  // basename
            case "bh3d":
                KerrGeodesic.fromJson().solve();
                break;
            case "newton":
                Newton.fromJson().solve();
                break;
            case "nbody3d":
                NBody.fromJson().solve();
                break;
            default:  // for debugging "utils" binary
                switch (args[1]) {  // command line argument
                    case "bh3d":
                        KerrGeodesic.fromJson().solve();
                        break;
                    case "newton":
                        Newton.fromJson().solve();
                        break;
                    case "nbody3d":
                        NBody.fromJson().solve();
                        break;
                    default:
                        stdout.printf("Please specify an executable by name or by program argument");
                        break;
                }
                break;
        }
        return 0;
    }
}

