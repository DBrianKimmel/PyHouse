// import Nevow.Athena.Test

Foo.Tests.OurFirstTest = Nevow.Athena.Test.TestCase.subclass('OurFirstTest');
Foo.Tests.OurFirstTest.methods(
    function run(self) {
        self.assertEquals('apple', 'orange');
    });
