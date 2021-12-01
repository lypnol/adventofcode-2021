def run(s)
    lines = s.map &:to_i
    last = lines[0]
    count = 0
    lines.each do |l|
        count += 1 if l > last
        last = l
    end
    count
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
