def run(s)
    lines = s.map &:to_i
    partial_sums = (0...lines.length-2).to_a.map do |i|
        lines[i..i+2].sum
    end
    last = partial_sums[0]
    count = 0
    partial_sums.each do |l|
        count += 1 if l > last
        last = l
    end
    count
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
