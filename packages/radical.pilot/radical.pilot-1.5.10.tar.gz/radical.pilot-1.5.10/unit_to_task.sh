
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/ComputeUnit/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/ComputePilot/Pilot/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/compute_pilot/pilot/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/compute_unit/task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/Compute Pilot/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/Compute Unit/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/(Compute) unit/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/(Compute) Unit/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/compute unit/task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/units/tasks/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/unit/task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/Unit/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/UNIT/TASK/g" $f; done
for f in `find . -name \*unit\*`; do u=$f; t=`echo $f | sed -e 's/unit/task/g'`; git mv $u $t; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/Task/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bCU\b/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bCUD\b/TD/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bCU\b/Task/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bcud\b/td/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bcuds\b/tds/g" $f; done
for f in `find . -type f | grep -v git`; do echo $f; sed -i -e "s/\bcu\b/t/g" $f; done
for f in `find tests -type f -name \*.py | grep -v git`; do echo $f; sed -i -e "s/\btasktest/unittest/g" $f; done

