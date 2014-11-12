# Project description and plan

## Motivation

When building circuitry in Minecraft, it is relatively easy to place down appropriate blocks and wiring. Getting them
to do what you want is the challenge. For those unfamiliar with Minecraft blocks, people may want a simple way to
translate mathematical statements (Boolean logic) into Minecraft circuitry. This project attempts to do just that. By
taking in Boolean logic statements, it will transform it into a Minecraft map containing the circuit for visualization.

## Language domain

The domain of this is people wishing to get a better feel for what their Boolean expressions do or who want a simple way
to migrate their ideas to Minecraft circuitry. This is a rather small audience, but it should be very useful for 
said audience.

## Language design

The design of this language would involve users typing in a statement in a standard form of 
<a href="http://en.wikipedia.org/wiki/Boolean_algebra#Operations">Boolean Algebra</a>. After a translation to an IR involving 
wrapper functions there should be a way to create a minecraft map with the standard forms of inputs, OR gates, and AND gates to 
produce the output.

## Example computations
xv(y^z) => OR(VAR(x), AND(VAR(y),VAR(z))) => Minecraft map file containing an empty world aside from the circuitry. This
final step is both the least related to DSLs and the most complex.
