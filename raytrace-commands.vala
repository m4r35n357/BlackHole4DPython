/*
Copyright (c) 2014, 2015, 2016, Ian Smith (m4r35n357)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
using GLib.Math;
using Json;

namespace Sim {

    public static Json.Object fromString (string input) {
        unowned Json.Object o;
        var p = new Parser();
        try {
            p.load_from_data(input);
            o = p.get_root().get_object();
        } catch (Error e) {
            stderr.printf("Unable to parse the input data: %s\n", e.message);
            return_if_reached();
        }
        return o;
    }

    public static int main (string[] args) {
        var angle = double.parse(args[1]) * PI / 180.0;
        var c = cos(angle);
        var s = sin(angle);
        var line = stdin.read_line();
        while (line != null) {
            var p = fromString(line);
            stdout.printf("%.9e %.1d ", p.get_double_member("tau"), 2);
            stdout.printf("%.9e %.9e %.9e %.9e ", p.get_double_member("r"), cos(p.get_double_member("th")), p.get_double_member("t"), p.get_double_member("ph"));
            stdout.printf("%.9e %.9e %.9e %.9e ", p.get_double_member("rP"), -sin(p.get_double_member("th")) * p.get_double_member("thP"), p.get_double_member("tP"), p.get_double_member("phP"));
            stdout.printf("%.9e %.1d %.1d %.9e ", -c, 0, 0, s);
            stdout.printf("%.9e %.1d %.1d %.9e ", s, 0, 0, c);
            stdout.printf("%.1d %.1d %.1d %.1d\n", 0, 1, 0, 0);
            line = stdin.read_line();
        }
        return 0;
    }
}
