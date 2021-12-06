#![allow(incomplete_features)]
#![feature(generic_const_exprs)]
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Matrix<const N: usize, const M: usize>([usize; N * M])
where
    [(); N * M]:;

impl<const N: usize, const M: usize> Matrix<N, M>
where
    [(); N * M]:,
{
    const fn mul<const P: usize>(&self, rhs: &Matrix<M, P>) -> Matrix<N, P>
    where
        [(); M * P]:,
        [(); N * P]:,
    {
        let mut new = Matrix([0; N * P]);
        let mut i = 0;
        while i < N {
            let mut j = 0;
            while j < P {
                let mut k = 0;
                while k < M {
                    new.0[P * i + j] += self.0[M * i + k] * rhs.0[P * k + j];
                    k += 1;
                }
                j += 1;
            }
            i += 1;
        }
        new
    }
}

impl<const N: usize> Matrix<N, N>
where
    [(); N * N]:,
{
    const fn clone(&self) -> Self {
        let mut new = Self([0; N * N]);
        let mut i = 0;
        while i < N {
            let mut j = 0;
            while j < N {
                new.0[N * i + j] = self.0[N * i + j];
                j += 1;
            }
            i += 1;
        }
        new
    }

    const fn identity() -> Self {
        let mut new = Self([0; N * N]);
        let mut i = 0;
        while i < N {
            new.0[N * i + i] = 1;
            i += 1;
        }
        new
    }

    const fn power(&self, mut exponent: usize) -> Self {
        let mut rest = Self::identity();
        if exponent == 0 {
            return rest;
        }
        let mut powers = self.clone();
        if exponent == 1 {
            return powers;
        }
        while exponent > 1 {
            if exponent % 2 == 1 {
                rest = rest.mul(&powers);
            }
            powers = powers.mul(&powers);
            exponent >>= 1;
        }
        rest.mul(&powers)
    }
}

const SIZE: usize = 9;
/// Matrice de transition:
/// 0    0 1 0 0 0 0 0 0 0
/// 1    0 0 1 0 0 0 0 0 0
/// 2    0 0 0 1 0 0 0 0 0
/// 3    0 0 0 0 1 0 0 0 0
/// 4    0 0 0 0 0 1 0 0 0
/// 5    0 0 0 0 0 0 1 0 0
/// 6    1 0 0 0 0 0 0 1 0
/// 7    0 0 0 0 0 0 0 0 1
/// 8    1 0 0 0 0 0 0 0 0
/// 
/// X(n+1) = MX
/// Last gen X_80 = M^80 * X
/// Total pop = (1 1 1 1 1 1 1 1 1) * X_80 = (1 1 1 1 1 1 1 1 1)*M^80 * X
#[rustfmt::skip]
mod unformatted {
    use super::*;
    pub(super) const M: Matrix<SIZE, SIZE> = Matrix([
        0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0]);
}
use unformatted::*;
const EXPONENT: usize = 80;
const M_80: Matrix<SIZE, SIZE> = M.power(EXPONENT);
const GENERATION: Matrix<1, SIZE> = Matrix([1, 1, 1, 1, 1, 1, 1, 1, 1]).mul(&M_80);

fn run(input: &str) -> usize {
    let mut x0 = Matrix::<SIZE, 1>([0; SIZE]);
    for s in input.split(',') {
        let num: usize = s.parse().unwrap();
        x0.0[num] += 1;
    }
    GENERATION.mul(&x0).0[0]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("3,4,3,1,2"), 5934)
    }
}
