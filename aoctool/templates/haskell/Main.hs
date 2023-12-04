-- Advent of Code
-- Date:     {{puzzle.date_string}}
-- Language: {{language}}

module Main where

import Data.Char (toLower)
import System.Environment (getArgs)

import Aoc{{puzzle.year}}{{'%02d' % puzzle.day}} (parse, part1, part2)


inputDataPath :: FilePath
inputDataPath = "{{input_data_path}}"

data Part = Part1 | Part2 deriving (Enum, Eq, Show)

solve :: Part -> IO (Maybe Int)
solve part = do
    let solver = if part == Part1 then part1 else part2
    inputData <- readFile inputDataPath
    let solution = case parse inputData of
                    Nothing    -> error "parse not implemented"
                    Just value -> solver value
    return solution

main :: IO ()
main = do
    args <- getArgs
    let part = toEnum $ read (head args) - 1
    solution <- solve part
    case solution of
        Nothing -> error $ toLower <$> show part ++ " not implemented"
        Just sol -> print sol
