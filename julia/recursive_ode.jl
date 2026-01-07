# recursive_ode.jl
using JSON

function derivative(x, y)
    return y
end

function recursive_euler(f, x, y, h, steps)
    if steps == 0
        return y
    end

    y_next = y + h * f(x, y)
    return recursive_euler(f, x + h, y_next, h, steps - 1)
end

# Read input from stdin
input = JSON.parse(read(stdin, String))

x0 = input["x0"]
y0 = input["y0"]
h  = input["step"]
n  = input["steps"]

result = recursive_euler(derivative, x0, y0, h, n)

output = Dict(
    "result" => result,
    "equation" => "dy/dx = y",
    "method" => "recursive_euler"
)

println(JSON.json(output))
