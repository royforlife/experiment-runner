using ProgressMeter
using CSV
using Distributed
addprocs()

@everywhere begin
    using SharedArrays  # Ensure SharedVector is available in each worker

    function calculate_entropy(filepath::String)
        byte_counts = zeros(Int, 256)
        total_bytes = 0

        open(filepath, "r") do f
            while !eof(f)
                byte = read(f, UInt8)
                byte_counts[byte + 1] += 1
                total_bytes += 1
            end
        end

        entropy = 0.0
        for count in byte_counts
            if count == 0
                continue
            end
            probability = count / total_bytes
            entropy -= probability * log2(probability)
        end

        return entropy
    end
end

function main()
    script_dir = dirname(@__FILE__)
	parent_dir = abspath(joinpath(script_dir, ".."))
	files_dir = joinpath(parent_dir, "select")

	files_name = readdir(files_dir)
	# files = filter(entry -> isfile(joinpath(parent_dir, entry)), all_entries)
    n = length(files_name)

    # Check if there are files to process
    if n == 0
        println("No files found in the parent directory.")
        return
    end
    
    # Update file paths to include parent directory for accurate reading
    files = [joinpath(files_dir, f) for f in files_name]

    entropies = SharedVector{Float64}(n)
    
    p = Progress(n, 1)  # Create a progress bar

    @sync @distributed for i in 1:n
        file = files[i]
        entropies[i] = calculate_entropy(file)
    end

    # Finish the progress bar outside the loop
    for _ in 1:n
        next!(p)
    end

    # Extract min and max entropy values and files
    min_entropy, min_index = findmin(entropies)
    max_entropy, max_index = findmax(entropies)

    min_file = files[min_index]
    max_file = files[max_index]

    # Ensure the CSV is written from the main process
    if myid() == 1
        results = [Pair(files_name[i], entropies[i]) for i in 1:n]
        CSV.write("entropy_results.csv", results)
    end

    println("\nMinimum entropy: $min_entropy in file $min_file")
    println("Maximum entropy: $max_entropy in file $max_file")
end

main()
